// window.onload = function (e) {
//     liff.init(function (data) {
//         initializeApp(data);
//     });
// };

// function initializeApp(data) {
//     document.getElementById("line_user_id").value = data.context.userId;
// }

function search() {
  var input = document.getElementById("searchInput");
  var filter = input.value.toLowerCase();
  var nodes = document.getElementsByClassName('target');

  for (i = 0; i < nodes.length; i++) {
    if (nodes[i].innerText.toLowerCase().includes(filter)) {
      nodes[i].style.display = "block";
    } else {
      nodes[i].style.display = "none";
    }
  }
}