# Contributing to Boundary Detection System

Thank you for your interest in contributing! Here's how you can help.

## Ways to Contribute

### 1. Report Bugs
Found an issue? Please create a GitHub Issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 2. Suggest Features
Have an idea? Open an Issue with the **feature request** label describing:
- What you want to add
- Why it would be useful
- Possible implementation approach

### 3. Improve Documentation
- Fix typos or unclear explanations
- Add more examples
- Improve code comments
- Create tutorials

### 4. Submit Code
1. **Fork** the repository
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the coding style
4. **Test thoroughly** before submitting
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add: brief description of changes"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with a detailed description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/boundary_detection.git
cd boundary_detection

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install pytest black flake8
```

## Coding Standards

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Naming**: Use clear, descriptive variable/function names
- **Comments**: Comment complex logic, not obvious code
- **Testing**: Write tests for new features

## Commit Message Format

```
[Type]: Brief description

- More details here if needed
- Bullet points work well

Fixes #123 (if closing an issue)
```

Types: `Add`, `Fix`, `Improve`, `Refactor`, `Docs`, `Test`

## Pull Request Guidelines

- Keep PRs focused on one feature/fix
- Write descriptive PR title and description
- Link related issues: "Fixes #123"
- Test on multiple videos if possible
- Update documentation if needed

## Code Review

All submissions require review before merging. Be open to feedback and suggestions!

## Questions?

- Check existing Issues/Discussions
- Read the [README](../README.md)
- Create a Discussion topic

## License

By contributing, you agree your code will be licensed under the same terms as the project.

---

**Happy coding!** 🎉
