"""
Custom finders that can be used together
with StaticFileStorage objects to find
files that should be collected by collectstatic.
"""
from os.path import abspath
from pathlib import Path
from typing import Union

import sass
from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage


class SimpleBuefyFinder(BaseFinder):
    """
    A custom Finder class to compile buefy to static files,
    and then return paths to those static files so they may be collected
    by the static collector.
    """

    def __init__(self):
        """Initialize the finder with user settings and paths."""

        # Try to get the Buefy settings. The user may not have created this dict.
        try:
            self.BUEFY_SETTINGS = settings.BUEFY_SETTINGS
        except AttributeError:
            self.BUEFY_SETTINGS = {}

        self.simple_buefy_path = Path(__file__).resolve().parent
        self.custom_scss = self.BUEFY_SETTINGS.get("custom_scss", [])
        self.variables = self.BUEFY_SETTINGS.get("variables", {})
        self.storage = FileSystemStorage(self.simple_buefy_path)

    def _get_buefy_css(self):
        """Compiles the buefy css file and returns its relative path."""

        # Start by unpacking the users custom variables
        scss_string = ""
        for var, value in self.variables.items():
            scss_string += f"${var}: {value};\n"

        # SASS wants paths with forward slash:
        sass_buefy_path = str(self.simple_buefy_path).replace('\\', '/')
        # Now load buefy
        scss_string += f'@import "{sass_buefy_path}/sass/buefy/buefy-build.scss";'

        # Store this as a css file
        if hasattr(sass, "libsass_version"):
            css_string = sass.compile(string=scss_string)
        else:
            # If the user has the sass module installed in addition to libsass,
            # warn the user and fail hard.
            raise UserWarning(
                "There was an error compiling your Buefy CSS. This error is "
                "probably caused by having the `sass` module installed, as the two modules "
                "are in conflict, causing django-simple-buefy to import the wrong sass namespace."
                "\n"
                "Please ensure you have only the `libsass` module installed, "
                "not both `sass` and `libsass`, or this application will not work."
            )

        css_path = self.simple_buefy_path / "css" / "buefy.css"

        with open(css_path, "w") as buefy_css:
            buefy_css.write(css_string)

        return "css/buefy.css"

    def _get_custom_css(self):
        """Compiles any custom-specified SASS and returns its relative path."""

        paths = []

        for scss_path in self.custom_scss:
            # Check that we can process this
            relative_path = self.find_relative_staticfiles(scss_path)

            if relative_path is None:
                if "static/" in scss_path:
                    relative_path = Path(scss_path.split("static/", 1)[-1])
                else:
                    raise ValueError(
                        "We couldn't figure out where the static directory for the given SCSS "
                        f"path is: \"{scss_path}\". If the given path doesn't contain "
                        "\"static/\", then you may need to add it to your STATICFILES_DIRS "
                        "setting."
                    )

            # SASS wants paths with forward slash:
            scss_path = str(scss_path).replace('\\', '/')

            # Now load up the scss file
            scss_string = f'@import "{scss_path}";'

            # Store this as a css file - we don't check and raise here because it would have
            # already happened earlier, during the Buefy compilation
            css_string = sass.compile(string=scss_string)

            css_path = self.simple_buefy_path / relative_path.parent
            css_path.mkdir(exist_ok=True)
            css_path = f"{css_path}/{relative_path.stem}.css"

            with open(css_path, "w") as css_file:
                css_file.write(css_string)

            paths.append(f"{relative_path.parent}/{relative_path.stem}.css")

        return paths

    def _get_buefy_js(self):
        """
        Return a list of all the js files that are needed by buefy.
        """

        paths = []
        js_folder = self.simple_buefy_path / "js"

        for path in js_folder.rglob("*.*"):
            rel_path = path.relative_to(js_folder)

            paths.append(
                f"js/{'/'.join(rel_path.parts)}"
            )

        return paths

    def find_relative_staticfiles(self, path: Union[str, Path]) -> Union[Path, None]:
        """
        Returns a given path, relative to one of the paths in STATICFILES_DIRS.

        Returns None if the given path isn't available within STATICFILES_DIRS.
        """

        if not isinstance(path, Path):
            path = Path(abspath(path))

        for directory in settings.STATICFILES_DIRS:
            directory = Path(abspath(directory))

            if directory in path.parents:
                return path.relative_to(directory)

    def find(self, path, all=False):
        """
        Given a relative file path, find an absolute file path.

        If the ``all`` parameter is False (default) return only the first found
        file path; if True, return a list of all found files paths.
        """

        absolute_path = str(self.simple_buefy_path / path)

        if all:
            return [absolute_path]
        return absolute_path

    def list(self, ignore_patterns):
        """
        Return a two item iterable consisting of
        the relative path and storage instance.
        """

        files = [self._get_buefy_css()]
        files.extend(self._get_custom_css())
        files.extend(self._get_buefy_js())

        for path in files:
            yield path, self.storage
