def unread_messages_count(request):
    if request.user.is_authenticated:
        count = request.user.received_messages.filter(is_read=False).count()
        return {'unread_messages_count': count}
    return {}