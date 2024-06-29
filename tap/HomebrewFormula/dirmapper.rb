class Dirmapper < Formula
    desc "A CLI tool to generate a directory structure mapping"
    homepage "https://github.com/nashdean/dirmap"
    url "https://github.com/nashdean/dirmap/archive/refs/tags/v1.0.5.tar.gz"
    sha256 "7339ffb4c0c3aefe48bdfea6f0e35e441cd73c953bdd2067d10e8874064d1cca"
    license "MIT"
  
    depends_on "python@3.12"
  
    def install
      bin.install "src/dirmapper/main.py" => "dirmap"
      system "pip3", "install", "-r", "requirements.txt"
      bin.install Dir["bin/*"]
    end
  
    test do
      system "#{bin}/dirmap", "--version"
    end
  end
  