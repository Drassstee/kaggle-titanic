ifeq ($(OS),Windows_NT)
	PY_SYS := python
	V_BIN := Scripts
	CLEAN_CMD := rmdir /s /q
	fix_path = $(subst /,\,$1)
else
	PY_SYS := python3
	V_BIN := bin
	CLEAN_CMD := rm -rf
	fix_path = $1
endif

V_NAME := tit_venv
RQ = requirements.txt

V_PY = $(V_NAME)/$(V_BIN)/python
V_PIP = $(V_NAME)/$(V_BIN)/pip
V_JUP = $(V_NAME)/$(V_BIN)/jupyter
TOUCH_F = $(V_NAME)/.installed

.PHONY: run setup clean
run: setup
	@echo "Starting Jupyter on :8891"
	@$(call fix_path,$(V_JUP)) notebook --port 8891 --NotebookApp.token='' --NotebookApp.password=''

setup: $(TOUCH_F)
$(TOUCH_F): $(V_NAME) $(RQ)
	@echo "Installing/Updating requirements"
	@$(call fix_path,$(V_PIP)) install --upgrade pip
	@$(call fix_path,$(V_PIP)) install -r $(RQ)
	@$(call fix_path,$(V_PY)) -c "open('$(TOUCH_F)','w').close()"
$(V_NAME):
	@echo "Creating virtual environment"
	@$(PY_SYS) -m venv $(V_NAME)
clean:
	@echo "Deleting virtual environment"
	@-$(CLEAN_CMD) $(call fix_path,$(V_NAME))