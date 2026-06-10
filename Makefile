APP = zap.py
PYTHON = python
REQ_FILE = requirements.txt

all: welcome compile_pyinstaller pyinstaller_clean


welcome:
	@$(PYTHON) -c "print('\n ███████╗ █████╗ ██████╗\n ╚══███╔╝██╔══██╗██╔══██╗\n   ███╔╝ ███████║██████╔╝\n  ███╔╝  ██╔══██║██╔═══╝\n ███████╗██║  ██║██║\n ╚══════╝╚═╝  ╚═╝╚═╝ PM\n\n Welcome zap makefile!\n')"

compile_pyinstaller:
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install pyinstaller
	@echo "Compiling with PyInstaller..."
	@$(PYTHON) -m pip install -r $(REQ_FILE)
	@$(PYTHON) -m PyInstaller --onefile --noconsole $(APP)

pyinstaller_clean:
	@echo "Cleaning PyInstaller build files..."
	@$(PYTHON) -c "import os, shutil; [shutil.rmtree(d) for d in ['build'] if os.path.exists(d)]; [os.remove(f) for f in os.listdir('.') if f.endswith('.spec')]"
	