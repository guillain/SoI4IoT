                    {% if nameList is defined %}
                      <select id="name" name="name" placeholder="Device Name" >
                      {% for i in nameList: %}
                       {% if view is defined %}
                          {% if i[0] in view[index] %}
                          <option value="{{ i[0] }}" selected>{{ i[0] }}</option>
                          {% else %}
                          <option value="{{ i[0] }}">{{ i[0] }}</option>
                          {% endif %}
                        {% else %}
                          <option value="{{ i[0] }}">{{ i[0] }}</option>
                        {% endif %}
                      {% endfor %}
                      </select>
                    {% else %}
                      <input type="text" name="name" id="name" placeholder="Name" value="{% if view is defined %}{{ view[index] }}{% endif %}"/>
                    {% endif %}
