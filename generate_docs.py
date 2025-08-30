#!/usr/bin/env python3
"""
HTML Documentation Generator for Traity Quiz App

This script generates comprehensive HTML documentation from Python docstrings
by scanning all Python files in the project and extracting class/function information.
"""

import os
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class DocumentationGenerator:
    """
    Generates HTML documentation from Python source files.

    This class scans Python files, extracts docstrings, and generates
    a comprehensive HTML documentation with navigation and search capabilities.
    """

    def __init__(self, root_path: str):
        """
        Initialize the documentation generator.

        Args:
            root_path (str): Root directory path of the Python project
        """
        self.root_path = Path(root_path)
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []

    def scan_project(self) -> None:
        """Scan all Python files in the project and extract documentation."""
        for py_file in self.root_path.rglob("*.py"):
            if self._should_include_file(py_file):
                self._process_file(py_file)

    def _should_include_file(self, file_path: Path) -> bool:
        """Determine if a file should be included in documentation."""
        # Skip common exclude patterns
        exclude_patterns = [
            "__pycache__", ".git", "node_modules", "dist", "build",
            "venv", "env", ".env", "tests", "test_", "_test.py"
        ]

        file_str = str(file_path)
        return not any(pattern in file_str for pattern in exclude_patterns)

    def _process_file(self, file_path: Path) -> None:
        """Process a single Python file and extract documentation."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the AST
            tree = ast.parse(content, filename=str(file_path))

            # Extract module info
            module_name = self._get_module_name(file_path)
            self.modules[module_name] = {
                'path': str(file_path.relative_to(self.root_path)),
                'classes': [],
                'functions': []
            }

            # Extract classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._extract_class_info(node, file_path)
                    if class_info:
                        self.classes.append(class_info)
                        self.modules[module_name]['classes'].append(class_info)

                elif isinstance(node, ast.FunctionDef) and not isinstance(node, ast.AsyncFunctionDef):
                    func_info = self._extract_function_info(node, file_path)
                    if func_info:
                        self.functions.append(func_info)
                        self.modules[module_name]['functions'].append(func_info)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path."""
        relative_path = file_path.relative_to(self.root_path)
        return str(relative_path).replace('.py', '').replace(os.sep, '.')

    def _extract_class_info(self, node: ast.ClassDef, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract class information from AST node."""
        docstring = ast.get_docstring(node)
        if not docstring:
            return None

        return {
            'name': node.name,
            'docstring': docstring,
            'module': self._get_module_name(file_path),
            'line_number': node.lineno,
            'methods': self._extract_methods(node),
            'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases]
        }

    def _extract_methods(self, class_node: ast.ClassDef) -> List[Dict[str, Any]]:
        """Extract method information from class."""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    methods.append({
                        'name': node.name,
                        'docstring': docstring,
                        'line_number': node.lineno,
                        'args': [arg.arg for arg in node.args.args if arg.arg != 'self']
                    })
        return methods

    def _extract_function_info(self, node: ast.FunctionDef, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract function information from AST node."""
        docstring = ast.get_docstring(node)
        if not docstring:
            return None

        return {
            'name': node.name,
            'docstring': docstring,
            'module': self._get_module_name(file_path),
            'line_number': node.lineno,
            'args': [arg.arg for arg in node.args.args]
        }

    def generate_html(self, output_path: str) -> None:
        """Generate HTML documentation file."""
        html_content = self._generate_html_content()
        output_file = Path(output_path)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Documentation generated: {output_file}")

    def _generate_html_content(self) -> str:
        """Generate the complete HTML content."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Traity Quiz App - Documentation</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Traity Quiz App Documentation</h1>
            <p>Complete API documentation generated from Python docstrings</p>
            <div class="stats">
                <span>📁 {len(self.modules)} Modules</span>
                <span>🏗️ {len(self.classes)} Classes</span>
                <span>⚡ {len(self.functions)} Functions</span>
            </div>
        </header>

        <nav class="sidebar">
            <input type="text" id="search" placeholder="🔍 Search classes and functions..." onkeyup="filterContent()">
            <div class="nav-section">
                <h3>📂 Modules</h3>
                <ul id="module-list">
                    {self._generate_module_nav()}
                </ul>
            </div>
        </nav>

        <main class="content">
            {self._generate_main_content()}
        </main>
    </div>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>"""

    def _get_css_styles(self) -> str:
        """Get CSS styles for the documentation."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }

        .container {
            display: flex;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
        }

        .stats span {
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }

        .sidebar {
            width: 300px;
            background: white;
            padding: 1rem;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            overflow-y: auto;
        }

        #search {
            width: 100%;
            padding: 0.5rem;
            margin-bottom: 1rem;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 0.9rem;
        }

        .nav-section h3 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.25rem;
        }

        .nav-section ul {
            list-style: none;
        }

        .nav-section li {
            margin: 0.25rem 0;
        }

        .nav-section a {
            color: #555;
            text-decoration: none;
            display: block;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            transition: background-color 0.2s;
        }

        .nav-section a:hover {
            background-color: #f8f9fa;
            color: #2c3e50;
        }

        .content {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }

        .module-section {
            background: white;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .module-header {
            background: #3498db;
            color: white;
            padding: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .module-header:hover {
            background: #2980b9;
        }

        .module-content {
            padding: 1rem;
        }

        .class-card, .function-card {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 5px;
        }

        .class-card {
            border-left-color: #e74c3c;
        }

        .function-card {
            border-left-color: #27ae60;
        }

        .class-name, .function-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }

        .class-name {
            color: #e74c3c;
        }

        .function-name {
            color: #27ae60;
        }

        .docstring {
            color: #555;
            margin-bottom: 1rem;
            line-height: 1.5;
        }

        .methods {
            margin-top: 1rem;
        }

        .method {
            background: white;
            padding: 0.5rem;
            margin: 0.5rem 0;
            border-radius: 3px;
            border-left: 3px solid #bdc3c7;
        }

        .method-name {
            font-weight: bold;
            color: #2c3e50;
        }

        .code-example {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }

        .toggle-btn {
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
        }

        .hidden {
            display: none;
        }

        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }

            .sidebar {
                width: 100%;
                order: 2;
            }

            .content {
                order: 1;
            }
        }
        """

    def _generate_module_nav(self) -> str:
        """Generate navigation HTML for modules."""
        nav_items = []
        for module_name, module_info in self.modules.items():
            class_count = len(module_info['classes'])
            func_count = len(module_info['functions'])

            nav_items.append(f"""
                <li>
                    <a href="#module-{module_name.replace('.', '-')}">
                        📄 {module_name}
                        <small>({class_count} classes, {func_count} functions)</small>
                    </a>
                </li>
            """)

        return "\n".join(nav_items)

    def _generate_main_content(self) -> str:
        """Generate main content HTML."""
        content_sections = []

        for module_name, module_info in self.modules.items():
            section_id = module_name.replace('.', '-')

            classes_html = ""
            for class_info in module_info['classes']:
                methods_html = ""
                for method in class_info['methods']:
                    methods_html += f"""
                        <div class="method">
                            <div class="method-name">⚡ {method['name']}({', '.join(method['args'])})</div>
                            <div class="docstring">{method['docstring'][:200]}...</div>
                        </div>
                    """

                classes_html += f"""
                    <div class="class-card">
                        <div class="class-name">🏗️ {class_info['name']}</div>
                        <div class="docstring">{class_info['docstring'][:300]}...</div>
                        {f'<div class="methods"><h4>Methods:</h4>{methods_html}</div>' if methods_html else ''}
                    </div>
                """

            functions_html = ""
            for func_info in module_info['functions']:
                functions_html += f"""
                    <div class="function-card">
                        <div class="function-name">⚡ {func_info['name']}({', '.join(func_info['args'])})</div>
                        <div class="docstring">{func_info['docstring'][:300]}...</div>
                    </div>
                """

            if classes_html or functions_html:
                content_sections.append(f"""
                    <section class="module-section" id="module-{section_id}">
                        <div class="module-header" onclick="toggleModule('{section_id}')">
                            <h2>📂 {module_name}</h2>
                            <button class="toggle-btn">▼</button>
                        </div>
                        <div class="module-content" id="content-{section_id}">
                            {classes_html}
                            {functions_html}
                        </div>
                    </section>
                """)

        return "\n".join(content_sections)

    def _get_javascript(self) -> str:
        """Get JavaScript for interactive features."""
        return """
        function toggleModule(moduleId) {
            const content = document.getElementById(`content-${moduleId}`);
            const button = content.previousElementSibling.querySelector('.toggle-btn');

            if (content.classList.contains('hidden')) {
                content.classList.remove('hidden');
                button.textContent = '▼';
            } else {
                content.classList.add('hidden');
                button.textContent = '▶';
            }
        }

        function filterContent() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const sections = document.querySelectorAll('.module-section');

            sections.forEach(section => {
                const header = section.querySelector('.module-header h2');
                const content = section.querySelector('.module-content');
                const text = (header.textContent + content.textContent).toLowerCase();

                if (text.includes(searchTerm)) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }

        // Initialize - hide all module contents except first
        document.addEventListener('DOMContentLoaded', function() {
            const sections = document.querySelectorAll('.module-section');
            sections.forEach((section, index) => {
                if (index > 0) {
                    const content = section.querySelector('.module-content');
                    const button = section.querySelector('.toggle-btn');
                    content.classList.add('hidden');
                    button.textContent = '▶';
                }
            });
        });
        """


def main():
    """Main function to generate documentation."""
    project_root = Path(__file__).parent
    generator = DocumentationGenerator(str(project_root))

    print("🔍 Scanning Python files...")
    generator.scan_project()

    print(f"📊 Found {len(generator.modules)} modules, {len(generator.classes)} classes, {len(generator.functions)} functions")

    output_path = project_root / "docs" / "api_documentation.html"
    output_path.parent.mkdir(exist_ok=True)

    print("📝 Generating HTML documentation...")
    generator.generate_html(str(output_path))

    print("✅ Documentation generated successfully!")
    print(f"📂 Output: {output_path}")


if __name__ == "__main__":
    main()
