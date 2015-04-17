Procedure for adding new corpus

1. Put articles folder into webapp root
2. Put *.csv file with page names into app root
3. In load_data.py management command change the corpus name at the top.
4. In views.py add the corpus name to the list in download view.
5. In settings.py set the LIMIT to be half the size of corpus + 1
6. Login to admin page, and for the users you want set the has_job field to 0.
7. Login for each user from step 6. That should evenly divide the job among those users.

TODO
1. Automate everything above. Do it in load_data.py management command.