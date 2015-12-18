################################################################################
# Project Makefile
#   Author: CptSpaceToaster
#   Email:  CptSpaceToaster@gmail.com
################################################################################

######### Fallen and can't get back up? #########
.PHONY: help
help:
	@echo "Quick reference for supported build targets."
	@echo "----------------------------------------------------"
	@echo "  help                          Display this message."
	@echo "----------------------------------------------------"
	@echo "  check-tools                   Check if this user has required build tools in its PATH."
	@echo "  hooks                         Install some useful git-hooks to help ensure safe commits."
	@echo "----------------------------------------------------"
	@echo "  test                          Run some tests!"
	@echo "----------------------------------------------------"
	@echo "  clean-all                     Clean everything!"
	@printf "  %-30s" "clean-$(VENV)"
	@echo "Clean the virtual environment, and start anew."
	@echo "  clean-hooks                   Clean and uninstall the git-hooks"
	@echo "  clean-pycache                 Clean up python's compiled bytecode objects in the package"

################################################################################
include config.mk

.PHONY: check-tools
check-tools: $(TOOL_DEPS)
check-%:
	@printf "%-15s" "$*"
	@command -v "$*" &> /dev/null; \
	if [[ $$? -eq 0 ]] ; then \
		echo -e $(GRN)"OK"$(NC); \
		exit 0; \
	else \
		echo -e $(RED)"Missing"$(NC); \
		exit 1; \
	fi

######### Virtual Environment #########
$(VENV) $(PYTHON):
	$(MAKE) check-tools
	test -d $(VENV) || python3.4 -m venv --without-pip $(VENV)

######### Pip #########
$(PIP): $(PYTHON)
	wget $(PIP_URL) -O - | $(PYTHON)

# This creates a dotfile for the requirements, indicating that they were installed
.$(REQUIREMENTS): $(PIP) $(REQUIREMENTS)
	test -s $(REQUIREMENTS) && $(PIP) install -Ur $(REQUIREMENTS) || :
	touch .$(REQUIREMENTS)

######### Git Hooks #########
.PHONY: hooks
hooks: .hooks

.hooks: hooks/*
	ln -sf ../../hooks/pre-commit .git/hooks/pre-commit
	ln -sf ../../hooks/pre-push .git/hooks/pre-push
	touch .hooks

.PHONY: test
test: $(PYTHON) .$(REQUIREMENTS)
	$(PYTHON) -m unittest discover -s $(PACKAGE)

.PHONY: run
run: $(PYTHON) .$(REQUIREMENTS)
	$(PYTHON) command_host.py -f $(LOG_DIR)

######### Cleaning supplies #########
.PHONY: clean
clean: clean-pycache
	rm -rf $(LOG_DIR)

.PHONY: clean-all
clean-all: clean-$(VENV) clean-hooks clean

.PHONY: clean-$(VENV)
clean-$(VENV):
	rm -rf $(VENV)
	rm -rf .$(REQUIREMENTS)

.PHONY: clean-hooks
clean-hooks:
	rm -rf .git/hooks/pre-commit
	rm -rf .git/hooks/pre-push
	rm -rf .hooks

.PHONY: clean-pycache
clean-pycache:
	find -path "*/__pycache__/*" -not -path "*/venv/*" -delete
	find -name "__pycache__" -not -path "*/venv/*" -type d -delete
