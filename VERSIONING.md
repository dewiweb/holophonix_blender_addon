# Version Management Guide

## Version Format
`MAJOR.FEATURE.BUGFIX` (e.g., 1.2.3)

## Version Number Rules

### Major Version (MAJOR)
- Increment for breaking changes
- Reset FEATURE and BUGFIX to 0
- Example: 1.2.3 → 2.0.0

### Feature Version (FEATURE)
- Increment for new features
- Reset BUGFIX to 0
- Example: 1.2.3 → 1.3.0

### Bugfix Version (BUGFIX)
- Increment for bug fixes
- Maintain MAJOR and FEATURE
- Example: 1.2.3 → 1.2.4

## Release Types

### Beta Releases
- Odd FEATURE numbers
- Example: 1.1.0, 1.3.0

### Stable Releases
- Even FEATURE numbers
- Example: 1.2.0, 1.4.0

## Development Process

1. **Feature Development**
   - Create feature branch from develop
   - Update version in `__init__.py`
   - Merge to develop for beta release

2. **Stable Releases**
   - Merge develop to main
   - Create release tag
   - Update changelog

3. **Hotfixes**
   - Create hotfix branch from main
   - Increment BUGFIX version
   - Merge to both main and develop

## Version Update Workflow

1. Update version in `__init__.py`
2. Commit with message: "Bump version to X.Y.Z"
3. Push changes to appropriate branch
4. Create release through GitHub workflow

## Best Practices

- Always update version before merging
- Document changes in CHANGELOG.md
- Follow semantic versioning principles
- Use descriptive commit messages