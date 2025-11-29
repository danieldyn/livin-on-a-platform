# Convention For Adding New Button Animation

- new directory must be created inside **buttons** directory (current subdirectory -> **button_images_01**)
    - keeping this naming format (e.g., **button_images01**, **button_images02**, ...) for the subdirectories is not mandatory, but it would be appreciated
- inside this new directory the image names must have the following format -> **img{xx}.{file_type}** (e.g., **img01.png**)
    - **xx** must be a number in 2-digit format (e.g., **01**, **02**, ..., **11**, ..., **22**) -> starting from 01
    - **file_type** is the file type, as the name suggests (e.g., **png**, **jpg**, ...)
- when using the **get_img** method, the **directory** and **image_file_type** arguments are strings (the directory cannot have ./ in front when being given as an argument)
