#ifndef LIB2DIPP__QUEUE_H_
#define LIB2DIPP__QUEUE_H_

#include <stdlib.h>

typedef struct lipp_QueueElement lipp_QueueElement;
struct lipp_QueueElement {
    void* data;
    lipp_QueueElement* next;
};

typedef struct lipp_Queue lipp_Queue;
struct lipp_Queue {
    size_t type;
    lipp_QueueElement* front;
    lipp_QueueElement* back;
    size_t size;
};

lipp_Queue* lipp_QueueCreate();
void lipp_QueueDestroy(lipp_Queue* self);

void lipp_QueuePush(lipp_Queue* self, void* data);
void lipp_QueuePop(lipp_Queue* self);

int lipp_QueueEmpty(lipp_Queue* self);

#endif /* LIB2DIPP__QUEUE_H_ */

