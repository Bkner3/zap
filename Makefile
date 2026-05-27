APP = zap.py
PYTHON = python
REQ_FILE = requirements.txt

all: welcome choose 

welcome:
	@$(PYTHON) -c "print('\n ███████╗ █████╗ ██████╗\n ╚══███╔╝██╔══██╗██╔══██╗\n   ███╔╝ ███████║██████╔╝\n  ███╔╝  ██╔══██║██╔═══╝\n ███████╗██║  ██║██║\n ╚══════╝╚═╝  ╚═╝╚═╝ PM\n\n Welcome zap makefile!\n')"

choose:
	@$(PYTHON) -c "print('Choose a compiler:\n [1]PyInstaller (simpler but slower) \n [2]Nuitka (faster but more complex (requires gcc ))\n')"
	@read -p "Enter your choice: " choice; \
	if [ "$$choice" = "1" ]; then \
		$(MAKE) compile_pyinstaller; \
	elif [ "$$choice" = "2" ]; then \
		$(MAKE) compile_nuitka; \
	else \
		echo "Invalid choice."; \
	fi

compile_pyinstaller:
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install pyinstaller
	@echo "Compiling with PyInstaller..."
	@$(PYTHON) -m pip install -r $(REQ_FILE)
	@$(PYTHON) -m PyInstaller --onefile --noconsole $(APP)

compile_nuitka:
	@echo "Compiling with Nuitka..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install nuitka
	@$(PYTHON) -m pip install -r $(REQ_FILE)
	@$(PYTHON) -m nuitka --onefile --windows-disable-console $(APP)

pyinstaller_clean:
	@echo "Cleaning PyInstaller build files..."
	@$(PYTHON) -c "import os, shutil; [shutil.rmtree(d) for d in ['build'] if os.path.exists(d)]; [os.remove(f) for f in os.listdir('.') if f.endswith('.spec')]"
	
nuitka_clean:
	@echo "Cleaning Nuitka build files..."
	@$(PYTHON) -c "import os, shutil; [shutil.rmtree(d) for d in ['__pycache__', 'build'] if os.path.exists(d)]; [os.remove(f) for f in os.listdir('.') if f.endswith('.bin')]"