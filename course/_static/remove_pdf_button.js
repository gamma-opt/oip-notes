/* The `quantecon_book_theme` template incorporates a "Download PDF" button that either
 * - prints the page (so that it can be saved as PDF), or
 * - if a `_pdf` path exist in the build process, points to the pdf file in there.
 * 
 * Our current plan is to make the PDF of the entire book available to download,
 * and using this button for that would be somewhat misleading, as one can easily assume 
 * it means download PDF of page.
 * I'm not sure if I can edit the template without forking the theme, so I wrote this.
 * 
 * This script is added to the header of every HTML file.
 * The removePdfButton function has two hardcoded elements:
 * - the toolbar class name, and
 * - the PDF button being the 12th item in that list.
 * 
 * The event listener makes sure the above function is called when the page is loaded.
 */

function removePdfButton() {
    const toolbar = document.getElementsByClassName("qe-toolbar__links")[0];
    const pdf_button = toolbar.childNodes[11];
    toolbar.removeChild(pdf_button);
}

document.addEventListener('DOMContentLoaded', removePdfButton, false);