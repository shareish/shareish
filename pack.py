if __name__ == "__main__":
    import pkg_resources, os, time

    for package in pkg_resources.working_set:
        print("%s: %s" % (package, time.ctime(os.path.getctime(package.location))))