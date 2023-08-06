..
## Package Description, Installation and usage guide.

```
Use cases : 
To create logfiles and write to multiple log files from the same script.
```

#1. Install package

```
pip install easymultilogging
```

#2. Usage

```
#CreateLogs is the class inside easymultilogging package that is to be imported.
from easymultilogging import CreateLogs as cl
```

#3. Arguments for CreateLogs class
```
**log_dest_dir** = *Path to the directory where the log file is to be saved.*
**log_file_name** = *Name of the log file. (The log file can be accessed at : 'log_dest_dir/log_file_name'*
**log_format** = *Can be defined while intiallizing the class object, however the default argument is '%(asctime)s %(name)-12s%(levelname)s:%(message)s'*
**log_set_level** = *User defined logging set levels. Default value = 'DEBUG'. See the section #3.1 for the other valid arguments that can be passed on.*
```

#3.1 - IMPORTANT : Log levels that can be assigned the 'log_set_level' variable are as follows.
```
Common Logging Levels
So what are these logging levels? Here are some common ones that you'll see, listed in order from most severe to least severe, and followed up by some that are meta-considerations. When logging from your application, follow these guidelines:

**FATAL** -- (log_set_level = 'FATAL')
*Fatal represents truly catastrophic situations, as far as your application is concerned. Your application is about to abort to prevent some kind of corruption or serious problem, if possible. This entry in the log should probably result in someone getting a 3 AM phone call.*

**ERROR** -- (log_set_level = 'ERROR')
*An error is a serious issue and represents the failure of something important going on in your application. Unlike FATAL, the application itself isn't going down the tubes. Here you've got something like dropped database connections or the inability to access a file or service. This will require someone's attention probably sooner than later, but the application can limp along.*

**WARN** -- (log_set_level = 'WARN')
*Now we're getting into the grayer area of hypotheticals. You use the WARN log level to indicate that you might have a problem and that you've detected an unusual situation. Maybe you were trying to invoke a service and it failed a couple of times before connecting on an automatic retry. It's unexpected and unusual, but no real harm done, and it's not known whether the issue will persist or recur. Someone should investigate warnings.*

**INFO** -- (log_set_level = 'INFO')
*Finally, we can dial down the stress level. INFO messages correspond to normal application behavior and milestones. You probably won't care too much about these entries during normal operations, but they provide the skeleton of what happened. A service started or stopped. You added a new user to the database. That sort of thing.*

**DEBUG** -- (log_set_level = 'DEBUG')
*With DEBUG, you start to include more granular, diagnostic information. Here, you're probably getting into "noisy" territory and furnishing more information than you'd want in normal production situations. You're providing detailed diagnostic information for fellow developers, sysadmins, etc.*

**TRACE** -- (log_set_level = 'TRACE')
*This is really fine-grained information-finer even than DEBUG. When you're at this level, you're basically looking to capture every detail you possibly can about the application's behavior. This is likely to swamp your resources in production and is seriously diagnostic.*

**ALL** -- (log_set_level = 'ALL')
*This is just what it sounds like. Log absolutely everything, including any custom logging levels that someone has defined.*

**OFF** -- (log_set_level = 'OFF')
*This is also just what it sounds like. Don't log anything at all.*


*For all other valid inputs, please refer "https://stackoverflow.com/questions/2031163/when-to-use-the-different-log-levels"*
```

#3. Sample script

```
#CreateLogs is the class inside easymultilogging package that is to be imported.
from easymultilogging import CreateLogs as cl

#Create an object of the class CreateLogs. 
# Lets go ahead and create objects 'p1,'p2' for our sample script 

p1 = cl(log_dest_dir = 'C:\Opex Projects\McD-Toys-master\Source', log_file_name = 'testpackage_29.txt', log_set_level = 'DEBUG')
p1.logger.debug("-------process : 1")
         
p2 = cl(log_dest_dir = 'C:/Opex Projects/McD-Toys-master/', log_file_name = 'testpackage_30s.txt')
p2.logger.info("------process : 2")

#p2.logger.info(subprocess.check_output[arg1,arg2]) is a good example of how the object can be used to capture subprocess execution logs as well !

```