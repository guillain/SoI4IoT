                        <select id="grp" name="grp" placeholder="Group" >
                          <option value=""></option>
                          {% for i in config.GROUP.split(' '): %}
                          {% if view is defined %}
                          {% if i in view[index] %}
                          <option value="{{i}}" selected>{{ i }}</option>
                          {% else %}
                          <option value="{{i}}">{{ i }}</option>
                          {% endif %}
                          {% else %}
                          <option value="{{i}}">{{ i }}</option>
                          {% endif %}
                          {% endfor %}
                        </select>

