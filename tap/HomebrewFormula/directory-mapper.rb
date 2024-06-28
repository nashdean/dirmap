class DirectoryMapper < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool to generate a directory structure mapping"
    homepage "https://github.com/nashdean/dirmap"
    url "https://files.pythonhosted.org/packages/your_package.tar.gz" # Update with the URL to your package
    sha256 "your_package_sha256_hash" # Update with the SHA256 of your package
    license "MIT"
  
    depends_on "python@3.12" # Ensure it matches the version you used
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/directory-mapper", "--help"
    end
  end
  