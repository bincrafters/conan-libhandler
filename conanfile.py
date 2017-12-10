#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class LibhandlerConan(ConanFile):
    name = "libhandler"
    version = "0.5"
    url = "https://github.com/bincrafters/conan-libhandler"
    description = "Libhandler implements algebraic effects and handlers in portable C99. Monads for free in C."
    license = "https://raw.githubusercontent.com/koka-lang/libhandler/master/license.txt"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    
    def source(self):
        source_url = "https://github.com/koka-lang/libhandler"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.build_vs()

    def package(self):
        self.copy(pattern="LICENSE")
        self.copy(pattern="*.h", dst="include", src=os.path.join("sources","inc"))
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        
    def build_vs(self):
        sln_path = os.path.join("sources", "ide","msvc","libhandler.sln")
        arch = "x86" if self.settings.arch == "x86" else "x64"
        command = tools.msvc_build_command(
            self.settings, 
            sln_path, 
            targets=[self.name],
            arch=arch,
            toolset=self.settings.compiler.toolset,
            force_vcvars=False
        )            
        self.output.info("Running command: " + command)
        self.run(command)