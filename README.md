# ICRAR MS Viewer

Visualization applet for casacore measurement sets.

## Architecture

### MVVM Pattern

Currently using MVVM where the view model never points to the view and only has the responsibility of observing and changing the model, data transformation through getter properties and notifying the view.

![MVVM](/images/the-classic-MVVM-design-pattern-diagram.png)
![MVVM Stack](/images/a-vertical-view-of-MVVMC-design-pattern.png)

This is in contrast to MVC (Massive View Controllers) where the controller is coupled to the view and model:

![MVC](/images/the-classic-MVC-pattern-diagram.png)
