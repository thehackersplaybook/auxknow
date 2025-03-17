install_packages() {
    echo "Installing requirements for testing."
    pip install -r requirements.txt || return 1
    echo "Installing auxknow package for testing."
    pip install . || return 1
    return 0
}

install_packages || exit 1
pytest --cov 