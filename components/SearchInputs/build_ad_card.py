import dash_mantine_components as dmc

from src.manager import Ad
from src.utils.logger import log_function


@log_function(track_memory=True)
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
            dmc.Anchor(
                dmc.Button(
                    "Open Ad",
                    color="blue",
                    fullWidth=True,
                    mt="md",
                    radius="md",
                ),
                href=ad.get("url", "#"), target="_blank"
            )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w=350,
    )
