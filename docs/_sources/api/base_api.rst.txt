.. _api-base-api:

==================
基础 API
==================

基本方法
==================


init
------------------

..  py:function:: init(context)

    【必须实现】

    初始化方法 - 在回测和实时模拟交易只会在启动的时候触发一次。你的算法会使用这个方法来设置你需要的各种初始化配置。 context 对象将会在你的算法的所有其他的方法之间进行传递以方便你可以拿取到。

    :param context: 策略上下文
    :type context: :class:`~StrategyContext` object

    :example:

    ..  code-block:: python

        def init(context):
            # cash_limit的属性是根据用户需求自己定义的，你可以定义无限多种自己随后需要的属性，ricequant的系统默认只是会占用context.portfolio的关键字来调用策略的投资组合信息
            context.cash_limit = 5000

handle_bar
------------------

..  py:function:: handle_bar(context, bar_dict)

    【必须实现】

    bar数据的更新会自动触发该方法的调用。策略具体逻辑可在该方法内实现，包括交易信号的产生、订单的创建等。在实时模拟交易中，该函数在交易时间内会每分钟被触发一次。

    :param context: 策略上下文
    :type context: :class:`~StrategyContext` object

    :param bar_dict: key为order_book_id，value为bar数据。当前合约池内所有合约的bar数据信息都会更新在bar_dict里面
    :type bar_dict: :class:`~BarDict` object

    :example:

    ..  code-block:: python

        def handle_data(context, api):
            # put all your algorithm main logic here.
            # ...
            api.order_target_percent(stocks, weights,prices)  
            # ...




交易相关函数
=================

..  module:: api.api
    :synopsis: API

submit_order - 自由参数下单「通用」
------------------------------------------------------

.. autofunction:: submit_order






