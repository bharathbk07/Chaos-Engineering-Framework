import textwrap

def display_framework_info():
    framework_name = "Chaos Engineering Framework"
    description = (
        "A Python-based framework that analyzes your project's source code or README.md "
        "using AI to suggest relevant chaos and performance experiments. Based on these "
        "suggestions, users can create and run chaos experiments using Chaos Toolkit to "
        "improve system resilience."
    )
    how_it_works = (
        "1. Analyze your project's source code or README.md using AI.\n"
        "2. Suggest relevant chaos and performance experiments based on the analysis.\n"
        "3. Allow users to create and run chaos experiments using Chaos Toolkit.\n"
        "4. Help improve system resilience through experiment results and insights."
    )
    created_by = "Created by Bharath Kumar M"

    box_width = 72

    def box_line(char='-'):
        return '+' + (char * (box_width - 2)) + '+'

    def box_content(text):
        lines = []
        for paragraph in text.split('\n'):
            wrapped = textwrap.wrap(paragraph, width=box_width - 4) or ['']
            for line in wrapped:
                lines.append('| ' + line.ljust(box_width - 4) + ' |')
        return '\n'.join(lines)

    content = (
        box_content(framework_name.upper()) + '\n' +
        box_content('') + '\n' +
        box_content("DESCRIPTION:") + '\n' +
        box_content(description) + '\n' +
        box_content('') + '\n' +
        box_content("HOW IT WORKS:") + '\n' +
        box_content(how_it_works) + '\n' +
        box_content('') + '\n' +
        box_content(created_by)
    )

    print(box_line())
    print(content)
    print(box_line())

# Example usage:
if __name__ == "__main__":
    display_framework_info()