PY=python
PIP=pip
ENTRY=zap.py
APP_NAME=zap

# Detecta sistema
ifeq ($(OS),Windows_NT)
    EXE=$(APP_NAME).exe
    RUN_CMD=dist\\$(EXE)
else
    EXE=$(APP_NAME)
    RUN_CMD=./dist/$(EXE)
endif

# Alvos fictícios (Evita conflitos com pastas de mesmo nome)
.PHONY: all clean install build run

# ----------------------------
# DEFAULT
# ----------------------------
all: clean install build

# ----------------------------
# LIMPAR
# ----------------------------
clean:
	-$(PY) -c "import shutil, os; [shutil.rmtree(x, ignore_errors=True) for x in ['build','dist','__pycache__']]"
	-$(PY) -c "import os; [os.remove(f) for f in os.listdir('.') if f.endswith('.spec')]"

# ----------------------------
# INSTALAR DEPENDÊNCIAS
# ----------------------------
install:
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

# ----------------------------
# BUILD
# ----------------------------
build:
	$(PY) -m PyInstaller --onefile --clean --noconfirm --name $(APP_NAME) $(ENTRY)

# ----------------------------
# RUN
# ----------------------------
run:
	$(RUN_CMD)