from cover_letter_builder import CoverLetterBuilder


def app():
    builder = CoverLetterBuilder()
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_downloads()


if __name__ == "__main__":
    app()