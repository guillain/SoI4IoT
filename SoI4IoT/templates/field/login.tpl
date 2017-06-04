                    {% if loginList is defined %}
                      <select id="login" name="login" placeholder="User Login" >
                      {% for i in loginList: %}
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
                      <input type="text" name="login" id="login" placeholder="User Login" value="{% if view is defined %}{{ view[index] }}{% endif %}" />
                    {% endif %}
