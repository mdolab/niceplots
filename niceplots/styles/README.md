New styles can be added here by making a new file.

### File naming

The filename must end in `.mplstyle`.
Whatever is before `.mplstyle` will be the string used to reference the style when users call `setStyle` or `styleContext`.

### File contents

There are only two NicePlots-specific stylesheet requirements:

1. The color cycle is specified using the `axes.prop_cycle` rcParam.
2. The name of each color in the color cycle is specified in the `keymap.help` rcParam.

The existing stylesheets can be used as a model.
