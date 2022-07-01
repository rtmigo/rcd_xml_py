from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_python_code('import rcd_xml')
        pkg.run_python_code('from rcd_xml import remove_xmlns')

    print("\nPackage is OK!")
