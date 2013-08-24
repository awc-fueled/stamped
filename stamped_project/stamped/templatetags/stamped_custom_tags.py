from django import template
import datetime

register = template.Library()

@register.tag(name="timePosted")
def do_time_since(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, date_to_format = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return TimeSinceNode(date_to_format)

class TimeSinceNode(template.Node):
    def __init__(self, date_to_format):
        self.date_to_format = template.Variable(date_to_format)
    def render(self, context):
        try:
            d = self.date_to_format.resolve(context)
            delta = datetime.datetime.now() - d
            return "Posted %s days %s minutes and %s seconds ago" %(delta.days, delta.seconds//3600, (delta.seconds//60)%60)
        except template.VariableDoesNotExist:
            return ''
 


# @register.tag(name="timeSince")
# def do_time_since(parser,token):
#     nodelist = parser.parse(('endupper',))
#     parser.delete_first_token()
    
#     return UpperNode(nodelist)
    
# class UpperNode(template.Node):
#     def __init__(self,nodelist):
#         self.nodelist = nodelist
        
#     def render(self,context):
#         output = self.nodelist.render(context)
        
#         return output.upper()
        