all: clean install build

PY=python
PIP=pip
ENTRY=zap.py
APP_NAME=zap

# ----------------------------
# LIMPAR
# ----------------------------
clean:
	python -c "import shutil; [shutil.rmtree(x, ignore_errors=True) for x in ['build','dist','__pycache__']]"
	del *.spec 2>nul || true

# ----------------------------
# INSTALAR DEPENDÊNCIAS
# ----------------------------
install:
	$(PIP) install -r requirements.txt

# ----------------------------
# BUILD EXE
# ----------------------------
build:
	pyinstaller --onefile $(ENTRY) --name $(APP_NAME)