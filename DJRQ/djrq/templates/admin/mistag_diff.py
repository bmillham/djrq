<%page args="original, reported"/>
% if original == reported:
 <td colspan="2">${original}</td>
% else:
<td>${original}</td><td><b>${reported}</b></td>
% endif
