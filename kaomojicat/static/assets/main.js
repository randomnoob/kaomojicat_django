// Init clipboard -- for more info, please read the offical documentation: https://clipboardjs.com/
clipboard = new ClipboardJS('btn-copy');

// Success action handler
clipboard.on('success', function (e) {
    const currentLabel = target.innerHTML;

    // Exit label update when already in progress
    if (target.innerHTML === 'Copied!') {
        return;
    }

    // Update button label
    target.innerHTML = 'Copied!';

    // Revert button label after 3 seconds
    setTimeout(function () {
        target.innerHTML = currentLabel;
    }, 3000)
});