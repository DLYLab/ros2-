import launch
import launch.launch_description_sources
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    action_declare_start_rqt = launch.actions.DeclareLaunchArgument(
        'start_up_rqt', default_value="false",
    )
    start_up_rqt = launch.substitutions.LaunchConfiguration('start_up_rqt', default="false")
        
    # 动作1-启动其他launch
    multisim_launch_path = [get_package_share_directory('turtlesim'), '/launch/', 'multisim.launch.py']
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch_description_source=launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_path
        )
    )

    # 动作2-打印数据
    action_log_info = launch.actions.LogInfo(msg=str(multisim_launch_path))

    # 动作3 - 执行进程
    action_topic_list = launch.actions.ExecuteProcess(
        condition = launch.conditions.IfCondition(start_up_rqt),
        cmd=['rqt'],
    )

    # 动作4 - 组织动作成组，把多个动作放到一组
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(period=2.0, actions=[action_include_launch]),
        # launch.actions.TimerAction(period=4.0, actions=[action_log_info]),
        launch.actions.TimerAction(period=4.0, actions=[action_topic_list]),
    ])

    return launch.LaunchDescription([
        action_declare_start_rqt,
        action_log_info,
        action_group,
    ])