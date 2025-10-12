import dash_mantine_components as dmc

from src.manager import Ad


def build_ad_card(ad: Ad):
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src=ad.get("img", "https://via.placeholder.com/300x160.png?text=No+Image"),
                    h=160,
                    alt="Norway",
                )
            ),
            dmc.Group(
                [
                    dmc.Text(ad.get("price", ""), fw=500),
                    dmc.Badge(ad.get("site", ""), color="pink"),
                ],
                justify="space-between",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "%s - %s" % (ad.get("keyfacts_children", "No keyfacts found"), ad.get("location", "No location found")),
                size="sm",
                c="dimmed",
            ),
            dmc.Flex([
                dmc.Anchor(
                    dmc.Button(
                        "Open",
                        color="blue",
                        size="sm",
                        radius="md",
                    ),
                    href=ad.get("url", "#"), target="_blank"
                ),
                dmc.Chip(
                    "Save",
                    id=f"save_ad_{ad.get('id', '')}",
                    color="blue",
                    size="sm",
                    radius="lg",
                    variant="light",
                ),
            ], gap="md", justify="space-between", align="center", mt="md"),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w=350,
    )
