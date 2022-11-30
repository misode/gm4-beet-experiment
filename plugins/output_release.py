from beet import Context


def beet_default(ctx: Context):
	ctx.data.save(
		path=f"release/{ctx.project_id}",
		overwrite=True,
	)
