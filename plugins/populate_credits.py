from beet import Context, TextFile
from typing import Any


def beet_default(ctx: Context):
	manifest = ctx.cache["gm4_manifest"].json
	contributors: dict[str, Any] = manifest.get("contributors", {})
	credits = next((m["credits"] for m in manifest.get("modules", []) if m["id"] == ctx.project_id), {})
	if credits is None or len(credits) == 0:
		return

	text = "# Credits\n"
	for title in credits:
		people = credits[title]
		if not isinstance(people, list) or len(people) == 0:
			continue
		text += f"\n## {title}\n"
		for p in people:
			contributor = contributors.get(p, { "name": p })
			name = contributor.get("name", p)
			links = contributor.get("links", [])
			if len(links) >= 1:
				text += f"- [{name}]({links[0]})\n"
			else:
				text += f"- {name}\n"
	ctx.data.extra["CREDITS.md"] = TextFile(text)
