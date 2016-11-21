        # to generate new one
        try:
            f = None
            # get doc 
            f = get_resouce_file(code)
            with ExLock("doc2pdf2swf"):
                # convert doc to pdf
                p1 = pipes.Template()
                p1.debug(settings.DEBUG)
                p1.append('unoconv -f pdf -o $OUT $IN', 'ff')
                p1.copy(f.name, outfilepath + ".pdf")  # 'ff' --> $IN $OUT

                # convert pdf to swf
                p2 = pipes.Template()
                p2.debug(settings.DEBUG)
                p2.append(
                    'pdf2swf -s languagedir=/usr/local/xpdf-chinese-simplified '
                    + '$IN -o $OUT', 'ff')
                p2.copy(outfilepath + ".pdf", outfilepath + ".swf")
        finally:
            if f:
                f.close()
