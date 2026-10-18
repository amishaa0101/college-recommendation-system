document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#recommend-form');
    const methodSelect = document.getElementById('method');
    const rankInput = document.getElementById('rank-input');
    const categoryInput = document.getElementById('category-input');
    const programInput = document.getElementById('program-input');
    const collegeInput = document.getElementById('college-input');
    const collegeList = document.getElementById('college-list');

    // This script is also loaded on About and Contact, which have no search form
    if (!form) {
        return;
    }

    function showInputsForMethod() {
        const byRank = methodSelect.value === 'rank_program';
        rankInput.style.display = byRank ? 'block' : 'none';
        categoryInput.style.display = byRank ? 'block' : 'none';
        programInput.style.display = byRank ? 'block' : 'none';
        collegeInput.style.display = byRank ? 'none' : 'block';
    }

    // Show the right inputs for the default method on page load
    showInputsForMethod();
    methodSelect.addEventListener('change', showInputsForMethod);

    // Clicking a result row opens that college's details page
    collegeList.addEventListener('click', function(event) {
        const cell = event.target.closest('td');
        if (cell) {
            const collegeName = cell.parentElement.cells[0].textContent.trim();
            window.location.href = `/college_info/${encodeURIComponent(collegeName)}`;
        }
    });

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const requestData = {
            method: 'POST',
            body: formData
        }
        try {
            const response = await fetch('/recommend', requestData);
            const htmlTable = await response.text();
            collegeList.innerHTML = htmlTable;
            collegeList.style.display = 'block';
        } catch (error) {
            console.error('Error fetching college data:', error);
        }
    });

});
