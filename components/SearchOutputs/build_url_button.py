import dash_mantine_components as dmc


def build_url_button(u_name, u_url):
    return dmc.Anchor(
        dmc.Button(
            u_name, 
            color="blue", 
            mt="md", 
            radius="md", 
            variant="outline"
        ), 
        href=u_url, 
        target="_blank"
    )