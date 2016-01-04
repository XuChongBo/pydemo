    thread = Thread(target=background_thread, kwargs={'type_list':type_list, 'job_name':job_name})
    thread.daemon = True
    thread.start()
    return render_template('monitor.html')



