import os
import re

import pytest
from conan import ConanFile
from conan.tools.microsoft.msbuilddeps import MSBuildDeps


class DummyConanFile(ConanFile):
    # Minimal ConanFile required for MSBuildDeps generation
    name = "dummy"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Provide dummy settings that mimic a Windows Visual Studio build
        self.settings.os = "Windows"
        self.settings.compiler = "visual_studio"
        self.settings.compiler.version = "16"
        self.settings.arch = "x86_64"
        # Required attributes for MSBuildDeps
        self.build_folder = str(kwargs.get("build_folder", "build"))
        self.source_folder = str(kwargs.get("source_folder", "src"))
        # Ensure the folders exist
        os.makedirs(self.build_folder, exist_ok=True)
        os.makedirs(self.source_folder, exist_ok=True)


def test_msbuilddeps_does_not_emit_invalid_z_flag(tmp_path):
    # Arrange: create a dummy conanfile in a temporary directory
    conanfile = DummyConanFile(build_folder=str(tmp_path / "build"),
                              source_folder=str(tmp_path / "src"))

    # Act: generate the MSBuild dependency files
    msdeps = MSBuildDeps(conanfile)
    msdeps.generate()

    # The generated props file is located in the build folder under "conan\\conandeps.props"
    props_path = os.path.join(conanfile.build_folder, "conan", "conandeps.props")
    assert os.path.isfile(props_path), f"Expected props file not found at {props_path}"

    # Read the content of the generated props file
    with open(props_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Assert: the content must not contain the invalid "/z" flag without an argument.
    # The buggy implementation emitted a line like "... /z ..." where /z had no following font name.
    # We check that there is no occurrence of "/z" followed only by whitespace or end‑of‑line.
    invalid_z_pattern = re.compile(r"/z(?=\s|$)")
    assert not invalid_z_pattern.search(content), (
        "Generated conandeps.props contains an invalid '/z' flag without a substitute font name."
    )
