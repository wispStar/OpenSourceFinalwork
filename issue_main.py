# coding = utf-8

import fetch
import summary

if __name__ == '__main__':
    project_url = "https://github.com/vacanza/python-holidays/"
    fetch.request_issue(project_url)
    summary.get_title_turns()
    summary.summary()