from beet import Context
import os
from pathlib import Path
import requests
import json

MODRINTH_API = "https://api.modrinth.com/v2"
AUTH_TOKEN_KEY = "BEET_MODRINTH_TOKEN"
SUPPORTED_GAME_VERSIONS = ["1.19", "1.19.1", "1.19.2", "1.19.3"]


def beet_default(ctx: Context):
	version = os.getenv("VERSION", "1.19")
	base_path = Path("release") / version
	file_name = f"{ctx.project_id}_{version}.zip"
	ctx.data.save(
		path=base_path / file_name,
		overwrite=True,
		zipped=True,
	)

	os.makedirs(base_path / ctx.project_id, exist_ok=True)
	for file in ["README.md", "CREDITS.md", "pack.png"]:
		if file in ctx.data.extra:
			ctx.data.extra[file].dump(base_path / ctx.project_id, file)

	# Publish to modrinth
	modrinth = ctx.meta.get("modrinth", None)
	auth_token = os.environ.get(AUTH_TOKEN_KEY, None)
	if modrinth and auth_token and ctx.project_version:
		modrinth_id = modrinth["project_id"]

		res = requests.get(f"{MODRINTH_API}/project/{modrinth_id}/version", headers={'Authorization': auth_token})
		if not (200 <= res.status_code < 300):
			if res.status_code == 404:
				print(f"[GM4] Cannot publish to modrinth project {modrinth_id} as it doesn't exist.")
			else:
				print(f"[GM4] Failed to get project versions: {res.status_code} {res.text}")
			return
		project_data = res.json()
		matching_version = next((v for v in project_data if v["version_number"] == ctx.project_version), None)
		if matching_version is not None:
			return

		with open(base_path / file_name, "rb") as f:
			file_bytes = f.read()

		game_versions = modrinth.get("minecraft", SUPPORTED_GAME_VERSIONS)
		res = requests.post(f"{MODRINTH_API}/version", headers={'Authorization': auth_token}, files={
			"data": json.dumps({
				"name": f"{ctx.project_name} {ctx.project_version}",
				"version_number": ctx.project_version,
				"dependencies": [],
				"game_versions": game_versions,
				"version_type": "release",
				"loaders": ["minecraft"],
				"featured": False,
				"project_id": modrinth_id,
				"file_parts": [file_name],
			}),
			file_name: file_bytes,
		})
		if not (200 <= res.status_code < 300):
			print(f"[GM4] Failed to publish new version version: {res.status_code} {res.text}")
			return
		print(f"[GM4] Successfully published {res.json()['name']}")
