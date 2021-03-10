---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: guideline
---

{% for a in site.guidelines %}
  <h2 class="{{ a.pk }} title" style="display: none">
      {{ a.name }}
  </h2>
{% endfor %}

<h2 class="title" style="display: none">Eu sou a página de guidelines</h2>

<script>
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('filter');
    if (myParam != null) {
        const filters = myParam.split(",")
        filters.forEach(showFiltered) 
    } else {
        showFiltered("title") 
    }

    function showFiltered(filter) {
        const test = document.querySelectorAll("."+filter)
        for (var i of test) {
            i.style.display = "block"
        }
    }

</script>