document.addEventListener("DOMContentLoaded", () => {
    // // Initialize CodeMirror for JSON1
    // const json1Editor = CodeMirror.fromTextArea(document.getElementById("json1"), {
    //     mode: "text/plain",
    //     theme: "idea",
    //     lineNumbers: true,
    //     lineWrapping: true,
    //     matchBrackets: true,
    //     autoCloseBrackets: true,
    // });
    const json1Editor = document.getElementById("json1").innerHTML;
    // // Initialize CodeMirror for JSON2
    // const json2Editor = CodeMirror.fromTextArea(document.getElementById("json2"), {
    //     mode: "text/plain",
    //     theme: "idea",
    //     lineNumbers: true,
    //     lineWrapping: true,
    //     matchBrackets: true,
    //     autoCloseBrackets: true,
    // });
    const json2Editor = document.getElementById("json2").innerHTML;

    const json1Text = json1Editor;// .getValue();
    const json2Text = json2Editor;// .getValue();

    // Use diff_match_patch to calculate the diff
    const dmp = new diff_match_patch();
    const diffs = dmp.diff_main(json1Text, json2Text);
    dmp.diff_cleanupSemantic(diffs);

    const json1CodeMirror = CodeMirror.fromTextArea(document.getElementById("json1"), {
        mode: "text/plain",
        theme: "idea",
        lineNumbers: true,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
    });
    json1CodeMirror.setValue('');
    const json2CodeMirror = CodeMirror.fromTextArea(document.getElementById("json2"), {
        mode: "text/plain",
        theme: "idea",
        lineNumbers: true,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
    });
    json2CodeMirror.setValue('');
    
    for (let idx = 0; idx < diffs.length; idx++) {
        const [operation, text] = diffs[idx];
        const textLinesCnt = (text.match(/\n/g) || []).length;
        if (operation === 0) {
            json1CodeMirror.replaceRange(text, CodeMirror.Pos(json1CodeMirror.lastLine()));
            json2CodeMirror.replaceRange(text, CodeMirror.Pos(json2CodeMirror.lastLine()));
        } else if (operation === -1) {
            const json1Start = json1CodeMirror.lastLine();
            if (idx < diffs.length - 1) {   
                const nextOperation = diffs[idx + 1]?.[0];
                const nextText = diffs[idx + 1]?.[1];
                if (nextOperation === 1) {
                    const editedTextLineCnt = (nextText.match(/\n/g) || []).length;
                    if (editedTextLineCnt > textLinesCnt) {
                        json1CodeMirror.replaceRange(text+'\n'.repeat(editedTextLineCnt-textLinesCnt), CodeMirror.Pos(json1Start));
                    } else {
                        json1CodeMirror.replaceRange(text, CodeMirror.Pos(json1Start));
                    }
                    const json1End = json1CodeMirror.lastLine();
                    for (let i = json1Start; i <= json1End; i++) {
                        json1CodeMirror.addLineClass(i, "background", "line-edited");
                    }
                } else if (nextOperation === 0) {
                    const deletedLineCnt = (text.match(/\n/g) || []).length;
                    const deletedLines = "\n".repeat(deletedLineCnt);
                    const json2Start = json2CodeMirror.lastLine();
                    json1CodeMirror.replaceRange(text, CodeMirror.Pos(json1Start));
                    json2CodeMirror.replaceRange(deletedLines, CodeMirror.Pos(json2Start));
                    const json2End = json2CodeMirror.lastLine();
                    
                    const json1End = json1CodeMirror.lastLine();

                    for (let i = json1Start; i <= json1End; i++) {
                        json1CodeMirror.addLineClass(i, "background", "line-deleted");
                    }
                    
                    for (let i = json2Start; i <= json2End; i++) {
                        json2CodeMirror.addLineClass(i, "background", "line-deleted");
                    }
                }
            }
        } else if (operation === 1) {
            const previousOperation = diffs[idx - 1]?.[0];
            const previousText = diffs[idx - 1]?.[1];

            const json2Start = json2CodeMirror.lastLine();
            json2CodeMirror.replaceRange(text, CodeMirror.Pos(json2Start));
            const json2End = json2CodeMirror.lastLine();

            
            if (previousOperation === -1) {
                for (let i = json2Start; i <= json2End; i++) {
                    json2CodeMirror.addLineClass(i, "background", "line-edited");
                }
            } else {
                const addedLineCnt = (text.match(/\n/g) || []).length;
                const addedLines = "\n".repeat(addedLineCnt);
                const json1Start = json1CodeMirror.lastLine();
                json1CodeMirror.replaceRange(addedLines, CodeMirror.Pos(json1Start));
                const json1End = json1CodeMirror.lastLine();
                for(let i = json1Start; i <= json1End; i++) {
                    json1CodeMirror.addLineClass(i, "background", "line-added");
                }
                for (let i = json2Start; i <= json2End; i++) {
                    json2CodeMirror.addLineClass(i, "background", "line-added");
                }
            }
        }
    
    }

    function syncScroll(editor1, editor2) {
        let isSyncing = false;

        function onScroll(source, target) {
            if (isSyncing) return;
            isSyncing = true;
            const sourceScrollInfo = source.getScrollInfo();
            target.scrollTo(sourceScrollInfo.left, sourceScrollInfo.top);
            isSyncing = false;
        }

        editor1.on("scroll", () => onScroll(editor1, editor2));
        editor2.on("scroll", () => onScroll(editor2, editor1));
    }

    syncScroll(json1CodeMirror, json2CodeMirror);
});