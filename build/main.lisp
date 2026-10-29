;;;; main.lisp -- builds the site: sbcl --script build/main.lisp [args]

;;; Reading

(defun read-lines (in)
  ;; Return every line of the stream IN as a list of strings.
  )

;;; Phase 1: blocks

(defun parse-blocks (lines)
  ;; Group LINES into a list of blocks, such as:
  ;;   (:heading 2 "Title")
  ;;   (:paragraph "Some *text*")
  ;;   (:code "go" "func main() {}")
  ;; A line's first characters say what it starts: "#", "```", "- ", "> ".
  ;; A blank line ends a paragraph.
  )

;;; Phase 2: inlines

(defun parse-inlines (text)
  ;; Split the TEXT of a paragraph or heading into strings and inline
  ;; elements, such as:
  ;;   "Some *text*" => ("Some " (:em "text"))
  ;; Scan for "*", "`", "[", and so on.
  )

;;; Phase 3: HTML

(defun escape-html (text)
  ;; Replace & < > in TEXT with &amp; &lt; &gt;. Code blocks and code spans
  ;; need this, or Go's "i < n" becomes the start of a tag.
  )

(defun render-inlines (inlines)
  ;; Return INLINES as an HTML string:
  ;;   ("Some " (:em "text")) => "Some <em>text</em>"
  )

(defun render-block (block)
  ;; Return BLOCK as an HTML string:
  ;;   (:heading 2 "Title") => "<h2>Title</h2>"
  ;; Headings and paragraphs go through parse-inlines and render-inlines.
  ;; Code blocks go through escape-html only.
  )

(defun md-to-html (file)
  ;; Return FILE as an HTML string: open it, read-lines, parse-blocks, then
  ;; render-block each block and join the results.
  ;; Every file starts with front matter (between +++ or --- lines). It will
  ;; come out as junk until PLAN.md step 3.
  )

(defun main (args)
  "Build the site. ARGS is the list of command-line arguments."
  (declare (ignore args))
  (md-to-html "content/go_code.md"))

(main (rest sb-ext:*posix-argv*))
