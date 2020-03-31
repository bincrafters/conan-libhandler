from conans import ConanFile, tools, MSBuild, AutoToolsBuildEnvironment
import os


class LibhandlerConan(ConanFile):
    name = "libhandler"
    version = "0.5"
    description = "Libhandler implements algebraic effects and handlers in portable C99. Monads for free in C."
    url = "https://github.com/bincrafters/conan-libhandler"
    homepage = "https://github.com/koka-lang/libhandler" 
    license = "MIT"
    generators = "visual_studio"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    
    def configure(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
    
    def source(self):
        source_url = "https://github.com/koka-lang/libhandler"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        
    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.build_vs()
        else:
            self.build_make()
            
    def package(self):
        self.copy(pattern="license.txt", dst="license", src=self._source_subfolder)
        include_folder = os.path.join(self._source_subfolder, "inc")
        self.copy(pattern="*.h", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        
    def build_vs(self):
        sln_path = os.path.join(self._source_subfolder, "ide","msvc","libhandler.sln")
        msbuild = MSBuild(self)
        msbuild.build(sln_path, targets=["libhandler"])

    def build_make(self):
        with tools.chdir(self._source_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure()
            autotools.make()