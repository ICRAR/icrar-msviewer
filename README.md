# icrar-msviewer

A casacore data visualization and profiling applet for radio astronomy datasets.

icrar-msviewer is built using PySide6 and licensed under the GNU General Public License Version 3.

## Usage

![MainWindow](/images/mainwindow.png)


MSViewer when installed can be launched via the following command:

`msviewer [ms_path1] [ms_path2] [...]`

* For development the application can be lauched from the entry point at `icrar/msviewer.py`

* Extracted Measurement Sets can be opened via `File->Open MS`

## Contributing

If you want to contribute to a project and make it better, your help is very welcome. Contributing is also a great way to learn more about social coding on Github, new technologies and and their ecosystems and how to make constructive, helpful bug reports, feature requests and the noblest of all contributions: a good, clean pull request.

### How to make a clean pull request

Look for a project's contribution instructions. If there are any, follow them.

* Create a personal fork of the project on Github.
Clone the fork on your local machine. Your remote repo on Github is called origin.
* Add the original repository as a remote called upstream.
If you created your fork a while ago be sure to pull upstream changes into your local repository.
* Create a new branch to work on! Branch from develop if it exists, else from master.
* Implement/fix your feature, comment your code.
* Follow the code style of the project, including indentation.
* If the project has tests run them!
* Write or adapt tests as needed.
* Add or change the documentation as needed.
* Squash your commits into a single commit with git's interactive rebase. Create a new branch if necessary.
* Push your branch to your fork on Github, the remote origin.
* From your fork open a pull request in the correct branch. Target the project's develop branch if there is one, else go for master!
* Once the pull request is approved and merged you can pull the changes from upstream to your local repo and delete your extra branch(es).

And last but not least: Always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.

## Architecture

#### Qt

For running the viewer PySide6 must be installed successfully which is runs on using Qt6 native libraries. Backwards compatibility with earlier version of Pyside and Qt may be supported in future.

#### MVVM Pattern

The project uses the MVVM architectural pattern where the view model never points to the view and only has the responsibility of observing the model, changing the model and data transformation through getter properties and notifying the view.

<img src="/images/the-classic-MVVM-design-pattern-diagram.png" width="600">

The scaled MVVM pattern forms the following object hierarchy:

<img src="/images/a-vertical-view-of-MVVMC-design-pattern.png" width="600">

This is in contrast to MVC where the controller is coupled to the view and model:

<img src="/images/the-classic-MVC-pattern-diagram.png" width="600">
