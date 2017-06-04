                      <select id="admin" name="admin" placeholder="Admin" >
                        {% if view is defined %}
                        {% if view[index] == 1 %}
                        <option value="1" selected>1</option>
                        <option value="0" >0</option>
                        {% else %}
                        <option value="1" >1</option>
                        <option value="0" selected>0</option>
                        {% endif %}
                        {% else %}
                        <option value="1" >1</option>
                        <option value="0" selected>0</option>
                        {% endif %}
                      </select>
