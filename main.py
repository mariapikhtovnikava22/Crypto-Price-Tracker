import click
import uvicorn

import settings


AppConfig = settings.AppConfig


@click.group()
def cli():
    pass


@cli.command(short_help="start web")
def start():
    uvicorn.run(
        "web.create_app:app",
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=True,
    )


if __name__ == "__main__":
    cli()
