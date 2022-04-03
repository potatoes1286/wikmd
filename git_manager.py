import datetime

from git import Repo, InvalidGitRepositoryError, GitCommandError, NoSuchPathError
from config import get_config


CONFIG = get_config()


def is_git_repo(path: str) -> bool:
    """
    Function that determines if the given path is a git repo.
    :return: True if is a repo, False otherwise.
    """
    try:
        _ = Repo(path).git_dir
        return True
    except (InvalidGitRepositoryError, NoSuchPathError):
        return False


class WikiRepoManager:
    """
    Class that manages the git repo of the wiki.
    The repo could be local or remote (it will be cloned) depending on the config settings.
    """

    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.repo: Repo = self.__git_repo_init()

    def __git_repo_init(self) -> Repo:
        """
        Function that initializes the git repo of the Wiki.
        :return: initialized repo
        """
        if is_git_repo(CONFIG["wiki_directory"]):
            git_repo = self.__get_existing_repo()
        else:
            if CONFIG["remote_url"]:  # if a remote url has been set, clone the repo
                git_repo = self.__git_clone_remote()
            else:
                git_repo = self.__git_new_local()

        # Configure git username and email
        if git_repo:  # if the repo has been initialized
            git_repo.config_writer().set_value("user", "name", "wikmd").release()
            git_repo.config_writer().set_value("user", "email", "wikmd@no-mail.com").release()

        return git_repo

    def __get_existing_repo(self) -> Repo:
        """
        Function that gets the existing repo in the wiki_directory.
        Could be local or remote.
        :return: Repo
        """
        git_repo = None
        try:
            self.flask_app.logger.info(f"Initializing existing repo >>> {CONFIG['wiki_directory']} ...")
            git_repo = Repo(CONFIG["wiki_directory"])
            git_repo.git.checkout()  # don't specify branch, it could be main or master
        except (InvalidGitRepositoryError, GitCommandError, NoSuchPathError) as e:
            self.flask_app.logger.error(f"Existing repo initialization failed >>> {str(e)}")

        return git_repo

    def __git_clone_remote(self) -> Repo:
        """
        Function that clones a remote git repo according to the remote_url and the wiki_directory set in the config.
        :return: Repo
        """
        git_repo = None
        try:
            self.flask_app.logger.info(f"Cloning >>> {CONFIG['remote_url']} ...")
            git_repo = Repo.clone_from(url=CONFIG["remote_url"], to_path=CONFIG["wiki_directory"])
        except (InvalidGitRepositoryError, GitCommandError, NoSuchPathError) as e:
            self.flask_app.logger.error(f"Cloning from remote repo failed >>> {str(e)}")
        return git_repo

    def __git_new_local(self) -> Repo:
        """
        Function that inits a new local git repo according to the wiki_directory set in the config.
        :return: Repo
        """
        git_repo = None
        try:
            self.flask_app.logger.info(f"Creating a new local repo >>> {CONFIG['wiki_directory']} ...")
            git_repo = Repo.init(path=CONFIG["wiki_directory"])
            git_repo.git.checkout("-b", "main")  # create a new (-b) main branch
        except (InvalidGitRepositoryError, GitCommandError, NoSuchPathError) as e:
            self.flask_app.logger.error(f"New local repo initialization failed >>> {str(e)}")
        return git_repo

    def __git_pull(self):
        """
        Function that pulls from the remote wiki repo.
        """
        try:
            # git pull
            self.flask_app.logger.info(f"Pulling from the repo >>> {CONFIG['wiki_directory']} ...")
            self.repo.git.pull()
        except Exception as e:
            self.flask_app.logger.info(f"git pull failed >>> {str(e)}")

    def __git_commit(self, page_name="", commit_type=""):
        """
        Function that commits changes to the wiki repo.
        :param commit_type: could be 'Add', 'Edit' or 'Remove'.
        :param page_name: name of the page that has been changed.
        """
        try:
            # git add --all
            self.repo.git.add("--all")
            date = datetime.datetime.now()
            commit_msg = f"{commit_type} page '{page_name}' on {str(date)}"
            # git commit -m
            self.repo.git.commit('-m', commit_msg)
            self.flask_app.logger.info(f"New git commit >>> {commit_msg}")
        except Exception as e:
            self.flask_app.logger.error(f"git commit failed >>> {str(e)}")

    def __git_push(self):
        """
        Function that pushes changes to the remote wiki repo.
        """
        try:
            # git push
            self.repo.git.push("-u", "origin", "master")
            self.flask_app.logger.info("Pushed to the repo.")
        except Exception as e:
            self.flask_app.logger.error(f"git push failed >>> {str(e)}")

    def git_sync(self, page_name="", commit_type=""):
        """
        Function that manages the synchronization with a git repo, that could be local or remote.
        If SYNC_WITH_REMOTE is set, it also pulls before committing and then pushes changes to the remote repo.
        :param commit_type: could be 'Add', 'Edit' or 'Remove'.
        :param page_name: name of the page that has been changed.
        """
        if CONFIG["sync_with_remote"]:
            self.__git_pull()

        self.__git_commit(page_name=page_name, commit_type=commit_type)

        if CONFIG["sync_with_remote"]:
            self.__git_push()
