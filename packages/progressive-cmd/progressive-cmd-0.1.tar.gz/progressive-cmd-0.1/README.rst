Progressive CMD
###############
Executes a cmd while interpreting its completion percentage.

The completion percentage of the cmd is stored in
an attribute ``percentage`` and the user can obtain percentage
increments by executing ``increment``  or by passing
a *callback* when initializing.

This class is useful to use within a child thread, so the child thread
executes the cmd, blocking and updating the increment and percentage
to the parent thread, that can do other things in the meantime.

Examples
********
Badblocks
=========

.. code-block:: python

  def my_callback(increment, total):
     print(f'Update: +{increment}% / {total}%.')

  def child_thread():
    progress = ProgressiveCmd('badblocks', '-st', 'random', '-w', 'dev/sda1', digits=ProgressiveCmd.DECIMALS, decimal_digits=2, read=35, callback=my_callback)
    progress.run()

  t = threading.Thread(target=child_thread)
  t.start()

Shred
=====

.. code-block:: python

  def my_callback(increment, total):
     print(f'Update: +{increment} / {total}%.')

  def child_thread():
    progress = ProgressiveCmd('shred', '-vn 1', 'dev/sda1', callback=my_callback)
    progress.run()

  t = threading.Thread(target=child_thread)
  t.start()

fsarchiver
==========

.. code-block:: python

  def my_callback(increment, total):
     print(f'Update: +{increment} / {total}%.')

  def child_thread():
    progress = ProgressiveCmd('fsarchiver', 'restfs', '-v', 'foo/bar/', 'id=0,dest=dev/sda1', callback=my_callback)
    progress.run()

  t = threading.Thread(target=child_thread)
  t.start()


Using tqdm
==========
You can use the ``increment`` value to update `tqdm <https://tqdm.github.io>`_:

.. code-block:: python

  t = tqdm(total=100)

  def my_callback(increment, total):
      t.update(increment)

  def child_thread():
    progress = ProgressiveCmd('a-program', callback=my_callback)
    progress.run()

  thread = threading.Thread(target=child_thread)
  thread.start()

Testing
*******
1. ``git clone`` this project.
2. Execute ``python setup.py test`` in the project folder.

Contributing
************
Is a missing or wrong code? Say it in the issues! Feel free to contribute.
