from beet import Context, LootTable


def beet_default(ctx: Context):
	ctx.generate("disassembly", LootTable({
		"pools": [
			{
				"rolls": 4,
				"entries": []
			}
		]
	}))
