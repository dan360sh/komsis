const COLLAPSER_CLASS = "crumble-title"
const COLLAPSER_ACTIVE_CLASS = "crumble-active"
const COLLAPSER_ACTIVE_TITLE_CLASS = "crumble-title-active"


function onCollapserClick(event) {
    var target = event.target;
    var collapserTargetId = target.dataset.target;
    var collapserTarget = document.getElementById(collapserTargetId)
    if(!collapserTarget){
        return;
    }
    var currentState = collapserTarget.classList.contains(COLLAPSER_ACTIVE_CLASS)
    // переключаем состояние collapserTarget, поэтому передаем 
    // состояние противоположное текущему
    toggleCollapserTarget(target, collapserTarget, currentState)
}

function toggleCollapserTarget(title, target, state) {
    if(state) {
        title.classList.remove(COLLAPSER_ACTIVE_TITLE_CLASS)
        target.classList.remove(COLLAPSER_ACTIVE_CLASS)
    } else {
        title.classList.add(COLLAPSER_ACTIVE_TITLE_CLASS)
        target.classList.add(COLLAPSER_ACTIVE_CLASS)
    }
}

var collapserBlocks = document.getElementsByClassName(COLLAPSER_CLASS);
if(collapserBlocks.length > 0) {
    for (var index = 0; index < collapserBlocks.length; index++) {
        var element = collapserBlocks[index];
        element.addEventListener("click", function(event) {
            onCollapserClick(event)
        })
    }
}
